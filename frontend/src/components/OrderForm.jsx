import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Alert,
  Box,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography
} from '@mui/material';

export default function OrderForm({ open, onClose, onSubmit, products, customers }) {
  const [formData, setFormData] = useState({
    customer_id: '',
    items: []
  });
  const [currentItem, setCurrentItem] = useState({
    product_id: '',
    quantity: ''
  });
  const [error, setError] = useState('');

  const handleCustomerChange = (e) => {
    setFormData(prev => ({
      ...prev,
      customer_id: parseInt(e.target.value) || ''
    }));
  };

  const handleProductChange = (e) => {
    setCurrentItem(prev => ({
      ...prev,
      product_id: parseInt(e.target.value) || ''
    }));
  };

  const handleQuantityChange = (e) => {
    setCurrentItem(prev => ({
      ...prev,
      quantity: parseInt(e.target.value) || ''
    }));
  };

  const addItem = () => {
    if (!currentItem.product_id || !currentItem.quantity) {
      setError('Please select product and quantity');
      return;
    }

    const product = products.find(p => p.id === currentItem.product_id);
    if (currentItem.quantity > product.stock_quantity) {
      setError(`Insufficient stock. Available: ${product.stock_quantity}`);
      return;
    }

    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { ...currentItem }]
    }));

    setCurrentItem({ product_id: '', quantity: '' });
    setError('');
  };

  const removeItem = (index) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async () => {
    if (!formData.customer_id || formData.items.length === 0) {
      setError('Please select customer and add items');
      return;
    }

    try {
      await onSubmit(formData);
      setFormData({ customer_id: '', items: [] });
      setError('');
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error creating order');
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create Order</DialogTitle>
      <DialogContent sx={{ pt: 2 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <TextField
          select
          fullWidth
          label="Customer"
          value={formData.customer_id}
          onChange={handleCustomerChange}
          margin="normal"
          required
          SelectProps={{
            native: true,
          }}
        >
          <option value="">Select a customer</option>
          {customers.map(customer => (
            <option key={customer.id} value={customer.id}>
              {customer.full_name} ({customer.email})
            </option>
          ))}
        </TextField>

        <Box sx={{ mt: 3, mb: 2 }}>
          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
            Add Items
          </Typography>
          
          <TextField
            select
            fullWidth
            label="Product"
            value={currentItem.product_id}
            onChange={handleProductChange}
            margin="normal"
            size="small"
            SelectProps={{
              native: true,
            }}
          >
            <option value="">Select a product</option>
            {products.map(product => (
              <option key={product.id} value={product.id}>
                {product.name} (${product.price}) - Stock: {product.stock_quantity}
              </option>
            ))}
          </TextField>
          
          <TextField
            fullWidth
            label="Quantity"
            type="number"
            value={currentItem.quantity}
            onChange={handleQuantityChange}
            margin="normal"
            size="small"
            inputProps={{ min: 1 }}
          />
          
          <Button onClick={addItem} variant="outlined" fullWidth sx={{ mt: 1 }}>
            Add Item
          </Button>
        </Box>

        {formData.items.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
              Order Items ({formData.items.length})
            </Typography>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Product</TableCell>
                  <TableCell align="right">Qty</TableCell>
                  <TableCell align="right">Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {formData.items.map((item, idx) => {
                  const product = products.find(p => p.id === item.product_id);
                  return (
                    <TableRow key={idx}>
                      <TableCell>{product?.name}</TableCell>
                      <TableCell align="right">{item.quantity}</TableCell>
                      <TableCell align="right">
                        <Button
                          size="small"
                          color="error"
                          onClick={() => removeItem(idx)}
                        >
                          Remove
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained" disabled={formData.items.length === 0}>
          Create Order
        </Button>
      </DialogActions>
    </Dialog>
  );
}
