import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { getAppliances, createAppliance, deleteAppliance } from '../api';

const applianceTypes = ["firewall", "manager", "manager_of_manager"];
const applianceFamilies = {
  firewall: ["fortigate", "palo_alto", "checkpoint_gateway"],
  manager: ["mds", "panorama", "fortimanager"],
  manager_of_manager: ["ruleblade"],
};


const Configuration = () => {
  const queryClient = useQueryClient();
  const [formState, setFormState] = useState({
    name: '',
    ip_address: '',
    appliance_type: 'firewall',
    appliance_family: 'fortigate',
    username: '',
    password: ''
  });

  const { data: appliances, isLoading, isError } = useQuery({
    queryKey: ['appliances'],
    queryFn: getAppliances,
  });

  const createMutation = useMutation({
    mutationFn: createAppliance,
    onSuccess: () => {
      toast.success('Appliance added successfully!');
      queryClient.invalidateQueries(['appliances']);
      document.getElementById('add_appliance_modal').close();
    },
    onError: (error) => {
      toast.error(`Failed to add appliance: ${error.response?.data?.detail || error.message}`);
    }
  });

  const deleteMutation = useMutation({
    mutationFn: deleteAppliance,
    onSuccess: () => {
      toast.success('Appliance deleted successfully!');
      queryClient.invalidateQueries(['appliances']);
    },
    onError: (error) => {
      toast.error(`Failed to delete appliance: ${error.message}`);
    }
  });
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormState(prevState => {
      const newState = { ...prevState, [name]: value };
      if (name === "appliance_type") {
        newState.appliance_family = applianceFamilies[value][0];
      }
      return newState;
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate(formState);
  };
  
  return (
    <div className="container mx-auto p-4 w-full">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Appliances Configuration</h1>
        <button className="btn btn-primary" onClick={() => document.getElementById('add_appliance_modal').showModal()}>Add Appliance</button>
      </div>

      {/* Add Appliance Modal */}
      <dialog id="add_appliance_modal" className="modal">
        <div className="modal-box">
          <form method="dialog">
            <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
          <h3 className="font-bold text-lg mb-4">Add a new Appliance</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input type="text" name="name" placeholder="Name" className="input input-bordered w-full" onChange={handleInputChange} value={formState.name} required />
            <input type="text" name="ip_address" placeholder="IP Address" className="input input-bordered w-full" onChange={handleInputChange} value={formState.ip_address} required />
            <select name="appliance_type" className="select select-bordered w-full" onChange={handleInputChange} value={formState.appliance_type}>
              {applianceTypes.map(type => <option key={type} value={type}>{type}</option>)}
            </select>
            <select name="appliance_family" className="select select-bordered w-full" onChange={handleInputChange} value={formState.appliance_family}>
              {applianceFamilies[formState.appliance_type].map(family => <option key={family} value={family}>{family}</option>)}
            </select>
            <input type="text" name="username" placeholder="Username" className="input input-bordered w-full" onChange={handleInputChange} value={formState.username} required />
            <input type="password" name="password" placeholder="Password" className="input input-bordered w-full" onChange={handleInputChange} value={formState.password} required />
            <button type="submit" className="btn btn-primary w-full" disabled={createMutation.isLoading}>
              {createMutation.isLoading ? 'Adding...' : 'Add Appliance'}
            </button>
          </form>
        </div>
      </dialog>

      {/* Appliances Table */}
      <div className="overflow-x-auto">
        <table className="table w-full">
          <thead>
            <tr>
              <th>Name</th>
              <th>IP Address</th>
              <th>Type</th>
              <th>Family</th>
              <th>Username</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && <tr><td colSpan="6" className="text-center">Loading...</td></tr>}
            {isError && <tr><td colSpan="6" className="text-center text-error">Error fetching data</td></tr>}
            {appliances?.data.map(appliance => (
              <tr key={appliance.id}>
                <td>{appliance.name}</td>
                <td>{appliance.ip_address}</td>
                <td>{appliance.appliance_type}</td>
                <td>{appliance.appliance_family}</td>
                <td>{appliance.username}</td>
                <td>
                  <button 
                    className="btn btn-ghost btn-xs"
                    onClick={() => deleteMutation.mutate(appliance.id)}
                    disabled={deleteMutation.isLoading}
                  >
                    delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Configuration; 