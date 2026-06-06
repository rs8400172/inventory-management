import { Box, Paper, Typography } from '@mui/material';

export default function StatCard({ title, value, color = '#1976d2' }) {
  return (
    <Paper sx={{ p: 3, textAlign: 'center', backgroundColor: color, color: 'white' }}>
      <Typography variant="body2" sx={{ mb: 1 }}>
        {title}
      </Typography>
      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
        {value}
      </Typography>
    </Paper>
  );
}
