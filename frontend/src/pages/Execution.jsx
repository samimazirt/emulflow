import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { getAppliances, createTest, startFortiTest } from '../api';

const TestExecution = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [selectedAppliances, setSelectedAppliances] = useState([]);
  const [intensity, setIntensity] = useState(10);

  const { data: appliancesData, isLoading: appliancesLoading } = useQuery({
    queryKey: ['appliances'],
    queryFn: getAppliances,
  });

  const createTestMutation = useMutation({
    mutationFn: createTest,
    onSuccess: (data) => {
      toast.success('Test started successfully!');
      queryClient.invalidateQueries(['tests']);
      setSelectedAppliances([]);
      navigate(`/tests/${data.data.id}`);
    },
    onError: (error) => {
      toast.error(
        `Failed to start test: ${error.response?.data?.detail || error.message}`
      );
    },
  });

  const handleApplianceToggle = (applianceId) => {
    setSelectedAppliances((prev) =>
      prev.includes(applianceId)
        ? prev.filter((id) => id !== applianceId)
        : [...prev, applianceId]
    );
  };

  const handleStartTest = () => {
    if (selectedAppliances.length === 0) {
      toast.error('Please select at least one appliance to test.');
      return;
    }

    const selectedAppliancesObjects = appliancesData?.data.filter((a) =>
      selectedAppliances.includes(a.id)
    );

    const hasFortiManager = selectedAppliancesObjects.some(
      (a) => a.appliance_family === 'fortimanager'
    );

    if (hasFortiManager) {
      startFortiTest({appliance_ids: selectedAppliances, intensity: intensity})
        .then(() => {
          toast.success('FortiManager stress test started!');
          queryClient.invalidateQueries(['tests']);
        })
        .catch((err) => {
          toast.error(`Failed to start FortiManager test: ${err.message}`);
          console.log(err)
        });
    } else {
      createTestMutation.mutate({
        appliance_ids: selectedAppliances,
        intensity: intensity,
      });
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">Start a New Test</h1>

      <div className="card bg-base-200 shadow-xl">
        <div className="card-body space-y-6">
          {/* Step 1: Select Appliances */}
          <div className="form-control w-full">
            <label className="label">
              <span className="label-text font-bold text-lg">1. Select Appliances</span>
            </label>
            <div className="h-48 overflow-y-auto border border-base-300 rounded-lg p-2 bg-base-100">
              {appliancesLoading ? (
                <div className="text-center p-4">
                  <span className="loading loading-spinner"></span>
                </div>
              ) : !appliancesData?.data || appliancesData.data.length === 0 ? (
                <div className="text-center p-4 flex flex-col items-center justify-center h-full">
                  <p className="mb-2">No appliances found.</p>
                  <Link to="/configuration" className="btn btn-xs btn-primary">
                    Add an Appliance
                  </Link>
                </div>
              ) : (
                appliancesData.data.map((appliance) => (
                  <label
                    key={appliance.id}
                    className="label cursor-pointer hover:bg-base-300 rounded"
                  >
                    <span className="label-text">
                      {appliance.name} ({appliance.ip_address})
                    </span>
                    <input
                      type="checkbox"
                      className="checkbox checkbox-primary"
                      checked={selectedAppliances.includes(appliance.id)}
                      onChange={() => handleApplianceToggle(appliance.id)}
                    />
                  </label>
                ))
              )}
            </div>
          </div>

          {/* Step 2: Set Intensity */}
          <div className="form-control w-full">
            <label className="label">
              <span className="label-text font-bold text-lg">2. Set Intensity</span>
            </label>
            <p className="text-center font-bold text-primary text-3xl my-2">{intensity}</p>
            <input
              type="range"
              min="1"
              max="100"
              value={intensity}
              onChange={(e) => setIntensity(Number(e.target.value))}
              className="range range-primary"
            />
            <div className="w-full flex justify-between text-xs px-2">
              <span>1 req/s</span>
              <span>100 req/s</span>
            </div>
          </div>

          {/* Step 3: Start Test */}
          <div className="card-actions pt-4">
            <button
              className="btn btn-primary btn-block btn-lg"
              onClick={handleStartTest}
              disabled={createTestMutation.isLoading || selectedAppliances.length === 0}
            >
              {createTestMutation.isLoading ? (
                <span className="loading loading-spinner"></span>
              ) : (
                'Launch Test'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestExecution;
