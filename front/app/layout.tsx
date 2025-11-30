import React from 'react';

import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';

import { GlobalProvider } from '@/app/providers';
// import '@mantine/core/styles.css';
import '@/app/styles/globals.css';
import { Footer, GlobalNavbar } from '@/widgets';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: {
    default: 'Japark.dev',
    template: '%s | Japark.dev | 기말고사',
  },
  description: '[기말고사] 테스트 실행 현황, 이슈, 성공률을 한 눈에 확인하는 대시보드입니다.',
  icons: {
    icon: '/ja_bg_favicon.png',
    shortcut: '/ja_bg_favicon.png',
    apple: '/ja_bg_favicon.png',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className="flex min-h-screen flex-col">
          <GlobalNavbar />
          <GlobalProvider>{children}</GlobalProvider>
          <Footer />
        </div>
      </body>
    </html>
  );
}
