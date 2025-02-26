import { createRoot } from 'react-dom/client';
import App from './App.tsx'; // Ruta relativa desde main.tsx
import './index.css';

const root = createRoot(document.getElementById('root')!);
root.render(<App />);