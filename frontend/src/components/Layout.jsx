import { AppBar, Toolbar, Typography, Box, Container } from '@mui/material';

export default function Layout({ children }) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            📦 Inventory Management System
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4, flex: 1 }}>
        {children}
      </Container>

      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: '#f5f5f5',
          textAlign: 'center',
          borderTop: '1px solid #ddd'
        }}
      >
        <Typography variant="body2" color="textSecondary">
          © 2026 Inventory Management System. All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
}
