import { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  CircularProgress,
  Alert,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography
} from '@mui/material';
import StatCard from '../components/StatCard';
import { dashboardService, productService } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const [statsRes, productsRes] = await Promise.all([
        dashboardService.getStats(),
        productService.getAll(0, 100)
      ]);
      setStats(statsRes.data);
      setProducts(productsRes.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 3 }}>
        📊 Dashboard
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      {stats && (
        <>
          {/* Statistics Cards */}
          <Grid container spacing={2} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Total Products"
                value={stats.total_products}
                color="#1976d2"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Total Customers"
                value={stats.total_customers}
                color="#388e3c"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Total Orders"
                value={stats.total_orders}
                color="#f57c00"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Low Stock Alerts"
                value={stats.low_stock_products.length}
                color="#c62828"
              />
            </Grid>
          </Grid>

          {/* Low Stock Products */}
          {stats.low_stock_products.length > 0 && (
            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                ⚠️ Low Stock Products (≤ {stats.low_stock_threshold} units)
              </Typography>
              <Paper>
                <Table>
                  <TableHead sx={{ backgroundColor: '#fff3cd' }}>
                    <TableRow>
                      <TableCell sx={{ fontWeight: 'bold' }}>ID</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Name</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>SKU</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 'bold' }}>Price</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 'bold' }}>Stock</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {stats.low_stock_products.map(product => (
                      <TableRow key={product.id} sx={{ backgroundColor: '#fff9e6' }}>
                        <TableCell>{product.id}</TableCell>
                        <TableCell>{product.name}</TableCell>
                        <TableCell>{product.sku}</TableCell>
                        <TableCell align="right">${product.price.toFixed(2)}</TableCell>
                        <TableCell align="right">
                          <Box sx={{
                            display: 'inline-block',
                            px: 1.5,
                            py: 0.5,
                            borderRadius: 1,
                            backgroundColor: '#ffcdd2',
                            color: '#c62828',
                            fontWeight: 'bold'
                          }}>
                            {product.stock_quantity}
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Paper>
            </Box>
          )}

          {/* Quick Info */}
          <Box sx={{ mt: 4, p: 2, backgroundColor: '#e3f2fd', borderRadius: 1, border: '1px solid #bbdefb' }}>
            <Typography variant="body2" color="textSecondary">
              💡 <strong>Quick Stats:</strong> You have {stats.total_products} products, {stats.total_customers} customers, and {stats.total_orders} orders in the system.
            </Typography>
          </Box>
        </>
      )}
    </Box>
  );
}
