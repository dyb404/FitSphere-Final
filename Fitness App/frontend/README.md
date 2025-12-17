# FitSphere Frontend

React + Vite frontend for the FitSphere fitness platform.

## Setup Instructions

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Access Application**
   - Frontend: http://localhost:5173
   - Make sure the backend is running on http://localhost:8000

## Features

- **Responsive Design**: Mobile-first approach with breakpoints at 768px and 1024px
- **Modern UI**: Clean, professional design with smooth animations
- **Role-Based Dashboards**: Different views for clients and trainers
- **Protected Routes**: Authentication and authorization handling
- **Interactive Components**: Carousel, modals, forms with validation
- **Real-time Updates**: Dynamic data fetching and state management

## Project Structure

```
frontend/
├── src/
│   ├── api/          # API functions
│   ├── components/   # Reusable components
│   ├── context/      # React Context (Auth)
│   ├── pages/        # Page components
│   ├── App.jsx       # Main app component
│   ├── main.jsx      # Entry point
│   └── styles.css    # Global styles
├── index.html
├── package.json
└── vite.config.js
```

## Demo Accounts

- **Trainer**: trainer@fitsphere.com / trainer123
- **Client**: client@fitsphere.com / client123

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

