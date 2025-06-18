import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { getFortiManagerStats } from '../api';

const fetchStats = async () => {
  const res = await getFortiManagerStats();
  return res.data;
};


const StatBox = ({ label, value, unit }) => (
  <div className="bg-base-200 rounded-xl p-4 text-center shadow">
    <p className="text-sm text-gray-400 mb-1">{label}</p>
    <p className="text-2xl font-bold">{value}{unit}</p>
  </div>
);

const parseUsagePercent = (usageString) => {
  if (!usageString) return "-";
  return parseFloat(usageString.replace("%", "")).toFixed(1);
};

const parseKbToGb = (kbString) => {
  if (!kbString) return "-";
  const kb = parseInt(kbString.replace(/,/g, "").replace(" KB", ""), 10);
  if (isNaN(kb)) return "-";
  return (kb / 1_048_576).toFixed(2);
};

const averageCpuUsage = (cpuData) => {
  if (!cpuData) return "-";
  const cores = Object.keys(cpuData).filter(key => key.startsWith("CPU[") && key.endsWith(" usage"));
  if (cores.length === 0) return "-";
  const usages = cores.map(core => {
    const usageStr = cpuData[core]?.Usage;
    return usageStr ? parseFloat(usageStr.replace("%", "")) : 0;
  });
  const avg = usages.reduce((a,b) => a+b, 0) / usages.length;
  return avg.toFixed(2);
};

const FortiStats = () => {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['fortimanager', 'stats'],
    queryFn: fetchStats,
    refetchInterval: 2000,
  });

  if (isLoading) return <p className="text-center">Loading FortiManager stats...</p>;
  if (isError) return <p className="text-center text-red-500">Error loading FortiManager stats</p>;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 my-4">
      <StatBox
        label="CPU Usage (avg cores)"
        value={averageCpuUsage(data.cpu)}
        unit="%"
      />
      <StatBox
        label="Memory Usage"
        value={parseUsagePercent(data.memory?.Used?.split(" ").pop())}
        unit="%"
      />
      <StatBox
        label="Flash Disk Usage"
        value={parseUsagePercent(data.flash_disk?.Used?.split(" ").pop())}
        unit="%"
      />
      <StatBox
        label="Flash Disk Size (GB)"
        value={parseKbToGb(data.flash_disk?.Total)}
        unit=" GB"
      />
      <StatBox
        label="Hard Disk Usage"
        value={parseUsagePercent(data.hard_disk?.Used?.split(" ").pop())}
        unit="%"
      />
      <StatBox
        label="Hard Disk Size (GB)"
        value={parseKbToGb(data.hard_disk?.Total)}
        unit=" GB"
      />
    </div>
  );
};

export default FortiStats;
