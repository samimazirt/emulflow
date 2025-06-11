import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTests } from '../api';
import { Link } from 'react-router-dom';

const RealTimeView = () => {
    const { data: testsData, isLoading } = useQuery({
        queryKey: ['tests'],
        queryFn: getTests,
        refetchInterval: 2000, // Refresh every 2 seconds for live feeling
        select: (data) => data.data.filter(t => t.status === 'running' || t.status === 'pending'),
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
                           <div className="flex justify-center my-4">
                               <span className="countdown font-mono text-4xl">
                                   <span style={{"--value": Math.floor((Date.now() - new Date(test.start_time).getTime()) / 1000 / 60)}}></span>
                                </span>
                               m
                                <span className="countdown font-mono text-4xl">
                                  <span style={{"--value": Math.floor((Date.now() - new Date(test.start_time).getTime()) / 1000 % 60)}}></span>
                                </span>
                               s
                           </div>
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