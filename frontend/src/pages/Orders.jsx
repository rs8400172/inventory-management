import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import OrderForm from '../components/OrderForm';
import { orderService, productService, customerService } from '../services/api';

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [openForm, setOpenForm] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [openDetails, setOpenDetails] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [ordersRes, productsRes, customersRes] = await Promise.all([
        orderService.getAll(0, 100),
        productService.getAll(0, 100),
        customerService.getAll(0, 100)
      ]);
      setOrders(ordersRes.data);
      setProducts(productsRes.data);
      setCustomers(customersRes.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = async (data) => {
    try {
      await orderService.create(data);
      await fetchData();
    } catch (err) {
      throw err;
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this order?')) {
      try {
        await orderService.delete(id);
        await fetchData();
      } catch (err) {
        setError('Failed to delete order');
      }
    }
  };

  const handleViewDetails = async (orderId) => {
    try {
      const response = await orderService.getById(orderId);
      setSelectedOrder(response.data);
      setOpenDetails(true);
    } catch (err) {
      setError('Failed to fetch order details');
    }
  };

  const getCustomerName = (customerId) => {
    return customers.find(c => c.id === customerId)?.full_name || 'Unknown';
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          🛒 Orders
        </Typography>
        <Button variant="contained" color="primary" onClick={() => setOpenForm(true)}>
          + Create Order
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Paper>
          <Table>
            <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold' }}>ID</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Customer</TableCell>
                <TableCell align="right" sx={{ fontWeight: 'bold' }}>Total Amount</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Date</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders.map(order => (
                <TableRow key={order.id} hover>
                  <TableCell>{order.id}</TableCell>
                  <TableCell>{getCustomerName(order.customer_id)}</TableCell>
                  <TableCell align="right">
                    <Box sx={{ fontWeight: 'bold', color: '#2e7d32' }}>
                      ${order.total_amount.toFixed(2)}
                    </Box>
                  </TableCell>
                  <TableCell>
                    {new Date(order.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      onClick={() => handleViewDetails(order.id)}
                      sx={{ mr: 1 }}
                    >
                      View
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDelete(order.id)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          {orders.length === 0 && (
            <Box sx={{ py: 4, textAlign: 'center' }}>
              <Typography color="textSecondary">No orders found</Typography>
            </Box>
          )}
        </Paper>
      )}

      {/* Order Details Dialog */}
      <Dialog open={openDetails} onClose={() => setOpenDetails(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Order Details #{selectedOrder?.id}</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          {selectedOrder && (
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                Customer: {getCustomerName(selectedOrder.customer_id)}
              </Typography>
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
                Total: ${selectedOrder.total_amount.toFixed(2)}
              </Typography>

              <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                Items:
              </Typography>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Product</TableCell>
                    <TableCell align="right">Qty</TableCell>
                    <TableCell align="right">Unit Price</TableCell>
                    <TableCell align="right">Subtotal</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {selectedOrder.items?.map((item, idx) => (
                    <TableRow key={idx}>
                      <TableCell>
                        {products.find(p => p.id === item.product_id)?.name || 'Unknown'}
                      </TableCell>
                      <TableCell align="right">{item.quantity}</TableCell>
                      <TableCell align="right">${item.unit_price.toFixed(2)}</TableCell>
                      <TableCell align="right">
                        ${(item.quantity * item.unit_price).toFixed(2)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDetails(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Order Form */}
      <OrderForm
        open={openForm}
        onClose={() => setOpenForm(false)}
        onSubmit={handleFormSubmit}
        products={products}
        customers={customers}
      />
    </Box>
  );
}
