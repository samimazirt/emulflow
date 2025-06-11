import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Configuration from './pages/Configuration';

// Placeholder pages for other routes
const Placeholder = ({ title }) => <div className="w-full text-center"><h1 className="text-4xl font-bold">{title}</h1></div>;


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Placeholder title="Real-time View" />} />
          <Route path="monitoring" element={<Placeholder title="Monitoring" />} />
          <Route path="execution" element={<Placeholder title="Test Execution" />} />
          <Route path="dashboard" element={<Placeholder title="Dashboard" />} />
          <Route path="configuration" element={<Configuration />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App; 