import React, { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTests } from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const { data: testsData, isLoading } = useQuery({
        queryKey: ['tests'],
        queryFn: getTests,
    });

    const chartData = useMemo(() => {
        if (!testsData?.data) return [];
        return testsData.data
            .filter(t => t.status === 'completed' && t.results)
            .slice(0, 10) // Get latest 10
            .map(test => ({
                name: `Test #${test.id}`,
                success: test.results.success || 0,
                failed: test.results.failed || 0,
            })).reverse(); // show oldest first
    }, [testsData]);

    const stats = useMemo(() => {
        if (!testsData?.data) return { totalTests: 0, totalSuccess: 0, totalFailed: 0, successRate: 0 };
        
        const completedTests = testsData.data.filter(t => t.status === 'completed' && t.results);
        const totalSuccess = completedTests.reduce((acc, t) => acc + (t.results.success || 0), 0);
        const totalFailed = completedTests.reduce((acc, t) => acc + (t.results.failed || 0), 0);
        const totalRequests = totalSuccess + totalFailed;

        return {
            totalTests: completedTests.length,
            totalSuccess,
            totalFailed,
            successRate: totalRequests > 0 ? ((totalSuccess / totalRequests) * 100).toFixed(1) : 0,
        };
    }, [testsData]);

    if (isLoading) {
        return <div className="text-center p-8"><span className="loading loading-lg"></span></div>;
    }

    if (chartData.length === 0) {
        return (
            <div className="text-center py-12">
                <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
                <p className="mb-4">No completed tests with results found.</p>
                <Link to="/execution" className="btn btn-primary">Run a Test</Link>
            </div>
        );
    }

    return (
        <div className="w-full p-4 space-y-8">
            <h1 className="text-3xl font-bold text-center">Dashboard</h1>

            {/* Stats */}
            <div className="stats shadow stats-vertical lg:stats-horizontal w-full">
                <div className="stat">
                    <div className="stat-title">Completed Tests</div>
                    <div className="stat-value">{stats.totalTests}</div>
                </div>
                <div className="stat">
                    <div className="stat-title">Successful Requests</div>
                    <div className="stat-value text-success">{stats.totalSuccess.toLocaleString()}</div>
                </div>
                <div className="stat">
                    <div className="stat-title">Failed Requests</div>
                    <div className="stat-value text-error">{stats.totalFailed.toLocaleString()}</div>
                </div>
                <div className="stat">
                    <div className="stat-title">Overall Success Rate</div>
                    <div className="stat-value">{stats.successRate}%</div>
                </div>
            </div>
            
            {/* Chart */}
            <div className="card bg-base-200 shadow-xl">
                <div className="card-body">
                    <h2 className="card-title">Recent Test Results</h2>
                    <div style={{ width: '100%', height: 400 }}>
                         <ResponsiveContainer>
                            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip wrapperClassName="card bg-base-100 p-2" />
                                <Legend />
                                <Bar dataKey="success" fill="#82ca9d" name="Success" />
                                <Bar dataKey="failed" fill="#ff7575" name="Failed" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 