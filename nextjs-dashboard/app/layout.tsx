import '@/app/ui/global.css';
import { AppRouterCacheProvider } from '@mui/material-nextjs/v13-appRouter';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <AppRouterCacheProvider>
        <body className="antialiased">{children}</body>
      </AppRouterCacheProvider>
    </html>
  );
}
