import './globals.css';

export const metadata = {
  title: 'F1 Pit Wall — AI Command Center',
  description: 'AI-powered Formula 1 analysis with multi-agent collaboration',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
