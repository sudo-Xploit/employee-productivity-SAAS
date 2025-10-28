# Frontend Integration Guide

This guide provides instructions and best practices for integrating the Employee Productivity API with your frontend application.

## Getting Started

### Prerequisites

- Node.js (v16+)
- npm or yarn
- Modern frontend framework (React, Vue, Angular, etc.)

### API Base URL

The API is available at:
- Development: `http://localhost:8000/api/v1`
- Production: Configure as needed in your environment

## Authentication Flow

### 1. User Registration and Login

Implement a registration and login form that collects:
- Email
- Password
- Full Name (for registration)
- Role (for registration, if applicable)

**Example Login Flow (React + Fetch):**

```jsx
const login = async (email, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    
    // Store tokens securely
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};
```

### 2. Token Management

Implement a token management system that:
- Stores access and refresh tokens securely
- Automatically refreshes the access token when expired
- Handles logout by clearing tokens

**Example Token Refresh (React + Axios):**

```jsx
import axios from 'axios';

// Create an axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// Add a request interceptor to include the token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If the error is 401 and we haven't retried yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('http://localhost:8000/api/v1/auth/refresh', {
          refresh_token: refreshToken,
        });
        
        const { access_token, refresh_token } = response.data;
        
        // Store the new tokens
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        
        // Update the authorization header
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
        
        // Retry the original request
        return axios(originalRequest);
      } catch (err) {
        // If refresh fails, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

## Role-Based Access Control

Implement role-based UI rendering based on the user's role:

```jsx
const RoleBasedComponent = ({ children, allowedRoles }) => {
  const userRole = useUserRole(); // Your custom hook to get user role
  
  if (!allowedRoles.includes(userRole)) {
    return null; // Or a "Not authorized" message
  }
  
  return children;
};

// Usage
<RoleBasedComponent allowedRoles={['ADMIN', 'DEPARTMENT_HEAD']}>
  <button>Create New Project</button>
</RoleBasedComponent>
```

## API Integration Examples

### Fetching Data

```jsx
// Using the api instance from above
const fetchDepartments = async () => {
  try {
    const response = await api.get('/departments');
    return response.data;
  } catch (error) {
    console.error('Error fetching departments:', error);
    throw error;
  }
};
```

### Creating Resources

```jsx
const createEmployee = async (employeeData) => {
  try {
    const response = await api.post('/employees', employeeData);
    return response.data;
  } catch (error) {
    console.error('Error creating employee:', error);
    throw error;
  }
};
```

### File Uploads

```jsx
const uploadCSV = async (entity, file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/upload/${entity}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Error uploading CSV:', error);
    throw error;
  }
};
```

### Downloading Reports

```jsx
const downloadReport = async (reportType) => {
  try {
    const response = await api.get(`/reports/generate?report_type=${reportType}`, {
      responseType: 'blob', // Important for file downloads
    });
    
    // Create a download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `report.${reportType}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    
  } catch (error) {
    console.error('Error downloading report:', error);
    throw error;
  }
};
```

## Analytics Dashboard Integration

For analytics dashboards, consider using:

1. **Chart.js** or **D3.js** for visualizations
2. **React Query** or similar for data fetching and caching
3. Implement auto-refresh for real-time updates

Example analytics data fetching:

```jsx
import { useQuery } from 'react-query';

const CompanyDashboard = () => {
  const { data, isLoading, error } = useQuery(
    'companyAnalytics', 
    () => api.get('/analytics/company').then(res => res.data),
    { refetchInterval: 60000 } // Refresh every minute
  );
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading analytics</div>;
  
  return (
    <div>
      <h1>Company Dashboard</h1>
      <div className="metrics-grid">
        <MetricCard title="Total Employees" value={data.total_employees} />
        <MetricCard title="Total Projects" value={data.total_projects} />
        <MetricCard title="ROI" value={`${(data.roi * 100).toFixed(2)}%`} />
        {/* More metrics */}
      </div>
      
      {/* Charts and visualizations */}
      <BarChart data={data.department_metrics} />
      <LineChart data={data.monthly_productivity} />
    </div>
  );
};
```

## ML Predictions Integration

For ML predictions, implement:

1. A prediction request system
2. Visualization of prediction results
3. Model training controls for admins

Example prediction component:

```jsx
const DepartmentPrediction = ({ departmentId }) => {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fetchPredictions = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/predict/department/${departmentId}`);
      setPredictions(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load predictions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const trainModel = async () => {
    setLoading(true);
    try {
      await api.post(`/predict/department/${departmentId}/train`);
      // Refresh predictions after training
      fetchPredictions();
    } catch (err) {
      setError('Failed to train model');
      console.error(err);
    }
  };
  
  useEffect(() => {
    fetchPredictions();
  }, [departmentId]);
  
  if (loading) return <div>Loading predictions...</div>;
  if (error) return <div>{error}</div>;
  if (!predictions) return null;
  
  return (
    <div className="predictions-container">
      <h2>Performance Predictions</h2>
      
      <div className="prediction-metrics">
        <PredictionCard 
          title="ROI Prediction"
          current={predictions.predictions.roi.current}
          predicted={predictions.predictions.roi.predicted}
          trend={predictions.predictions.roi.trend_percentage}
          confidence={predictions.predictions.roi.confidence}
        />
        
        <PredictionCard 
          title="Cost Prediction"
          current={predictions.predictions.cost.current}
          predicted={predictions.predictions.cost.predicted}
          trend={predictions.predictions.cost.trend_percentage}
          confidence={predictions.predictions.cost.confidence}
        />
      </div>
      
      <div className="recommendations">
        <h3>AI Recommendations</h3>
        <ul>
          {predictions.recommendations.map((rec, index) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
      </div>
      
      {/* Only show for admins */}
      <RoleBasedComponent allowedRoles={['ADMIN']}>
        <button onClick={trainModel} disabled={loading}>
          Train Model
        </button>
      </RoleBasedComponent>
    </div>
  );
};
```

## Error Handling

Implement consistent error handling:

```jsx
const ErrorBoundary = ({ children }) => {
  const [error, setError] = useState(null);
  
  // Global error handler
  useEffect(() => {
    const handleError = (error) => {
      console.error('API Error:', error);
      
      // Handle specific error codes
      if (error.response) {
        switch (error.response.status) {
          case 401:
            // Redirect to login if not handled by interceptor
            break;
          case 403:
            setError('You do not have permission to access this resource');
            break;
          case 404:
            setError('The requested resource was not found');
            break;
          case 500:
            setError('An internal server error occurred. Please try again later.');
            break;
          default:
            setError('An unexpected error occurred');
        }
      } else {
        setError('Network error. Please check your connection.');
      }
    };
    
    // Register global error handler
    api.interceptors.response.use(
      (response) => response,
      (error) => {
        handleError(error);
        return Promise.reject(error);
      }
    );
  }, []);
  
  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={() => setError(null)}>Dismiss</button>
      </div>
    );
  }
  
  return children;
};
```

## CORS Configuration

The backend is configured to accept requests from:
- http://localhost:3000
- http://127.0.0.1:3000
- http://localhost:5173
- http://127.0.0.1:5173

If you need to add additional origins, ask the backend developer to update the `cors.json` file.

## Health Check Integration

Implement a system status component:

```jsx
const SystemStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/health');
        const data = await response.json();
        setStatus(data);
      } catch (error) {
        console.error('Health check failed:', error);
        setStatus({ status: 'unhealthy', error: error.message });
      } finally {
        setLoading(false);
      }
    };
    
    checkHealth();
    const interval = setInterval(checkHealth, 60000); // Check every minute
    
    return () => clearInterval(interval);
  }, []);
  
  if (loading) return <div>Checking system status...</div>;
  
  const isHealthy = status && status.status === 'healthy';
  
  return (
    <div className={`system-status ${isHealthy ? 'healthy' : 'unhealthy'}`}>
      <h3>System Status: {isHealthy ? 'Healthy' : 'Unhealthy'}</h3>
      {!isHealthy && <p>Error: {status?.error || 'Unknown error'}</p>}
      
      {status && (
        <div className="status-details">
          <p>API Version: {status.version}</p>
          <p>CPU Usage: {status.resources?.cpu_usage}%</p>
          <p>Memory Usage: {status.resources?.memory?.percent_used}%</p>
          <p>Database: {status.database?.status}</p>
        </div>
      )}
    </div>
  );
};
```

## Best Practices

1. **State Management**: Use Redux, Zustand, or Context API for global state
2. **Data Fetching**: Use React Query, SWR, or Apollo Client for efficient data fetching
3. **Form Handling**: Use Formik or React Hook Form for form validation
4. **Type Safety**: Consider using TypeScript for better type safety
5. **Testing**: Implement unit and integration tests with Jest and React Testing Library
6. **Responsive Design**: Ensure all components work on mobile and desktop
7. **Accessibility**: Follow WCAG guidelines for accessibility
8. **Performance**: Implement code splitting and lazy loading for better performance

## Common Issues and Solutions

### CORS Errors

If you encounter CORS errors:
1. Ensure your frontend is running on an allowed origin
2. Check that you're including the correct headers in your requests
3. Contact the backend developer to update the CORS configuration if needed

### Authentication Issues

If you have authentication problems:
1. Check that you're storing and sending tokens correctly
2. Ensure your token refresh mechanism is working
3. Verify that your logout functionality clears all tokens

### Data Loading Performance

If data loading is slow:
1. Implement pagination for large data sets
2. Use caching strategies with React Query or similar
3. Consider implementing server-side filtering and sorting

## Contact

For backend API questions or issues, contact the backend development team.
