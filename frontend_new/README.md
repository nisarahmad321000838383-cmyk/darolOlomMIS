# School MIS Frontend

Modern React TypeScript frontend with Tailwind CSS, dark mode support, and comprehensive features for school management.

## 🚀 Features

- **Modern UI** with Tailwind CSS
- **Dark/Light Mode** with persistent theme
- **Role-Based Access** (SuperAdmin, Admin, Teacher, Student)
- **Fully Responsive** design
- **Type-Safe** with TypeScript
- **State Management** with Zustand
- **Data Fetching** with React Query
- **Form Validation** with React Hook Form + Zod
- **Beautiful Icons** with Lucide React
- **Toast Notifications** with React Hot Toast

## 📋 Requirements

- Node.js 18+
- npm or yarn

## 🛠️ Installation

1. **Install dependencies:**
```bash
cd frontend_new
npm install
```

2. **Create `.env` file:**
```bash
cp .env.example .env
```

3. **Start development server:**
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 🏗️ Project Structure

```
frontend_new/
├── src/
│   ├── components/        # Reusable UI components
│   │   └── ui/           # Base UI components
│   ├── features/         # Feature-specific components
│   ├── layouts/          # Layout components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── store/            # Zustand stores
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── package.json
└── vite.config.ts
```

## 🔑 Default Credentials

- **Super Admin**: `username: superadmin`, `password: Admin@123`

## 🎨 Theme

Toggle between light and dark mode using the theme button in the header. The theme preference is saved in localStorage.

## 📦 Build for Production

```bash
npm run build
```

The production build will be in the `dist` folder.

## 🧪 Linting

```bash
npm run lint
```

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔗 API Integration

The frontend connects to the Django backend at `http://localhost:8000` (configurable in `.env`).

## 📄 License

MIT License
