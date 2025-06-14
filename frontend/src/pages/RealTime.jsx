import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTests } from '../api';
import { Link } from 'react-router-dom';

const LiveTimer = ({ startTime }) => {
  const [elapsed, setElapsed] = React.useState(() => Date.now() - new Date(startTime).getTime());

  React.useEffect(() => {
    const interval = setInterval(() => {
      setElapsed(Date.now() - new Date(startTime).getTime());
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  const minutes = Math.floor(elapsed / 1000 / 60);
  console.log(minutes)
  const seconds = Math.floor((elapsed / 1000) % 60);

  return (
    <div className="flex flex-col items-center my-4">
      <div className="flex justify-center items-center gap-1">
        <p className='font-mono text-4xl'>{`${minutes}`}</p>

        <span className="text-2xl">m</span>
        <span className="countdown font-mono text-4xl">
          <span style={{ "--value": String(seconds) }}></span>
        </span>
        <span className="text-2xl">s</span>
      </div>
      <p className="text-sm mt-2 text-gray-500">
        {`Elapsed ms: ${elapsed} (${minutes}m ${seconds}s)`}
      </p>
    </div>
  );
};



const RealTimeView = () => {
    const { data: testsData, isLoading } = useQuery({
    queryKey: ['tests'],
    queryFn: getTests,
    refetchInterval: 2000,
    select: (data) => {
        const filtered = data.data.filter(t => t.status === 'running' || t.status === 'pending');
        console.log('Tests filtrés (running/pending) :', filtered);
        return filtered;
    },
});


    if (isLoading) {
        return <div className="text-center p-8"><span className="loading loading-lg"></span></div>;
    }

    if (!testsData || testsData.length === 0) {
        return (
            <div className="text-center py-12">
                <h1 className="text-3xl font-bold mb-4">Real-time View</h1>
                <p className="mb-4">No tests are currently running.</p>
                <Link to="/execution" className="btn btn-primary">Start a New Test</Link>
            </div>
        );
    }

    const getStatusBadge = (status) => {
        const colors = {
            pending: 'badge-info',
            running: 'badge-primary',
        };
        return <span className={`badge ${colors[status] || 'badge-ghost'}`}>{status}</span>;
    };

    return (
        <div className="w-full p-4 space-y-8">
            <h1 className="text-3xl font-bold text-center">Live Tests</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {testsData.map(test => (
                    <div key={test.id} className="card bg-base-200 shadow-xl">
                        <div className="card-body">
                            <div className="flex justify-between items-center mb-2">
                                <h2 className="card-title">Test #{test.id}</h2>
                                {getStatusBadge(test.status)}
                            </div>
                            <LiveTimer startTime={test.start_time} />
                            <p><span className="font-bold">Intensity:</span> {test.intensity} req/s</p>
                            <p><span className="font-bold">Appliances:</span> {test.appliances.map(a => a.name).join(', ')}</p>
                            <div className="card-actions justify-end mt-4">
                                <Link to={`/tests/${test.id}`} className="btn btn-secondary">
                                    View Details
                                </Link>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RealTimeView;
