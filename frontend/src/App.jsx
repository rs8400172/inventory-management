import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Box, Button } from '@mui/material';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Customers from './pages/Customers';
import Orders from './pages/Orders';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
          <Button
            component={Link}
            to="/"
            variant="outlined"
          >
            Dashboard
          </Button>
          <Button
            component={Link}
            to="/products"
            variant="outlined"
          >
            Products
          </Button>
          <Button
            component={Link}
            to="/customers"
            variant="outlined"
          >
            Customers
          </Button>
          <Button
            component={Link}
            to="/orders"
            variant="outlined"
          >
            Orders
          </Button>
        </Box>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/products" element={<Products />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/orders" element={<Orders />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
