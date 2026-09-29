import "./globals.css";
import Link from "next/link";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body>
    <div className="top"><Link href="/scans"><strong>Devkit</strong></Link><Link href="/scans">Scans</Link><Link href="/login">Account</Link></div>
    {children}
  </body></html>);
}
