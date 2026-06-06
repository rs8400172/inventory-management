import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Alert
} from '@mui/material';

export default function ProductForm({ open, onClose, onSubmit, initialData = null }) {
  const [formData, setFormData] = useState(
    initialData || {
      name: '',
      sku: '',
      price: '',
      stock_quantity: ''
    }
  );
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'price' || name === 'stock_quantity' ? parseFloat(value) || '' : value
    })); 
  };

  const handleSubmit = async () => {
    if (!formData.name || !formData.sku || !formData.price) {
      setError('Please fill all required fields');
      return;
    }

    try {
      await onSubmit(formData);
      setFormData({ name: '', sku: '', price: '', stock_quantity: '' });
      setError('');
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Error saving product');
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {initialData ? 'Edit Product' : 'Add Product'}
      </DialogTitle>
      <DialogContent sx={{ pt: 2 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <TextField
          fullWidth
          label="Product Name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          margin="normal"
          required
        />
        
        <TextField
          fullWidth
          label="SKU"
          name="sku"
          value={formData.sku}
          onChange={handleChange}
          margin="normal"
          required
          disabled={!!initialData}
        />
        
        <TextField
          fullWidth
          label="Price"
          name="price"
          type="number"
          inputProps={{ step: '0.01' }}
          value={formData.price}
          onChange={handleChange}
          margin="normal"
          required
        />
        
        <TextField
          fullWidth
          label="Stock Quantity"
          name="stock_quantity"
          type="number"
          value={formData.stock_quantity}
          onChange={handleChange}
          margin="normal"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">
          {initialData ? 'Update' : 'Add'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
