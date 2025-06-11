import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getTest } from '../api';

const TestDetail = () => {
    const { id } = useParams();
    const { data: testData, isLoading, isError } = useQuery({
        queryKey: ['test', id],
        queryFn: () => getTest(id),
        refetchInterval: (query) => {
            const test = query.state.data?.data;
            return test?.status === 'running' || test?.status === 'pending' ? 2000 : false;
        },
    });

    if (isLoading) return <div className="text-center"><span className="loading loading-lg"></span></div>;
    if (isError) return <div className="text-center text-error">Error fetching test details.</div>;

    const { data: test } = testData;

    const getStatusBadge = (status) => {
        const colors = {
          pending: 'badge-info',
          running: 'badge-primary',
          completed: 'badge-success',
          failed: 'badge-error',
          stopped: 'badge-warning',
        };
        return <span className={`badge ${colors[status] || 'badge-ghost'}`}>{status}</span>;
      };

    return (
        <div className="container mx-auto p-4 w-full">
            <Link to="/execution" className="btn btn-ghost mb-4">
                &larr; Back to Test Execution
            </Link>

            <div className="card bg-base-200 shadow-xl">
                <div className="card-body">
                    <div className="flex justify-between items-start">
                        <h1 className="card-title text-3xl">Test #{test.id}</h1>
                        {getStatusBadge(test.status)}
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-center">
                        <div className="stat">
                            <div className="stat-title">Intensity</div>
                            <div className="stat-value">{test.intensity} req/s</div>
                        </div>
                        <div className="stat">
                            <div className="stat-title">Start Time</div>
                            <div className="stat-value text-lg">{new Date(test.start_time).toLocaleString()}</div>
                        </div>
                        <div className="stat">
                            <div className="stat-title">End Time</div>
                            <div className="stat-value text-lg">{test.end_time ? new Date(test.end_time).toLocaleString() : 'N/A'}</div>
                        </div>
                    </div>

                    <div className="divider"></div>

                    <h2 className="text-xl font-bold">Tested Appliances</h2>
                    <div className="overflow-x-auto">
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>IP Address</th>
                                    <th>Type</th>
                                    <th>Family</th>
                                </tr>
                            </thead>
                            <tbody>
                                {test.appliances.map(app => (
                                    <tr key={app.id}>
                                        <td>{app.name}</td>
                                        <td>{app.ip_address}</td>
                                        <td>{app.appliance_type}</td>
                                        <td>{app.appliance_family}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    <div className="divider"></div>
                    
                    <h2 className="text-xl font-bold">Results</h2>
                    {test.status === 'completed' && test.results && (
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-center">
                            <div className="stat bg-base-300 rounded-box">
                                <div className="stat-title">Successful Requests</div>
                                <div className="stat-value text-success">{test.results.success}</div>
                            </div>
                            <div className="stat bg-base-300 rounded-box">
                                <div className="stat-title">Failed Requests</div>
                                <div className="stat-value text-error">{test.results.failed}</div>
                            </div>
                        </div>
                    )}

                    {test.status === 'failed' && test.results?.error && (
                        <div className="alert alert-error">
                            <div>
                                <span>Test failed: {test.results.error}</span>
                            </div>
                        </div>
                    )}

                    {test.results?.details && (
                        <>
                            <h3 className="text-lg font-bold mt-4">Execution Log</h3>
                            <pre className="bg-base-300 p-4 rounded-box max-h-96 overflow-y-auto">
                                <code>
                                    {test.results.details.join('\\n')}
                                </code>
                            </pre>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TestDetail; 