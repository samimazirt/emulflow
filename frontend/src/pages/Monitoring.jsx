import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTests } from '../api';
import { Link } from 'react-router-dom';

const Monitoring = () => {
    const { data: testsData, isLoading } = useQuery({
        queryKey: ['tests'],
        queryFn: getTests,
        select: (data) => data.data.filter(t => t.status !== 'running' && t.status !== 'pending'),
    });
    
    const getStatusBadge = (status) => {
        const colors = {
          completed: 'badge-success',
          failed: 'badge-error',
          stopped: 'badge-warning',
        };
        return <span className={`badge ${colors[status] || 'badge-ghost'}`}>{status}</span>;
    };

    if (isLoading) {
        return <div className="text-center p-8"><span className="loading loading-lg"></span></div>;
    }

    return (
        <div className="w-full p-4">
            <h1 className="text-3xl font-bold text-center mb-8">Test History</h1>
            <div className="overflow-x-auto">
                <table className="table w-full">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Status</th>
                            <th>Intensity</th>
                            <th>Start Time</th>
                            <th>End Time</th>
                            <th>Appliances</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading && <tr><td colSpan="7" className="text-center"><span className="loading loading-spinner"></span></td></tr>}
                        {!isLoading && (!testsData || testsData.length === 0) && (
                            <tr><td colSpan="7" className="text-center py-8">No test history found.</td></tr>
                        )}
                        {testsData?.map(test => (
                            <tr key={test.id} className="hover">
                                <th>{test.id}</th>
                                <td>{getStatusBadge(test.status)}</td>
                                <td>{test.intensity} req/s</td>
                                <td>{new Date(test.start_time).toLocaleString()}</td>
                                <td>{test.end_time ? new Date(test.end_time).toLocaleString() : 'N/A'}</td>
                                <td>{test.appliances.map(a => a.name).join(', ')}</td>
                                <td>
                                    <Link to={`/tests/${test.id}`} className="btn btn-ghost btn-xs">
                                        Details
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Monitoring; 