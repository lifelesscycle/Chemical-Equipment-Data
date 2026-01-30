import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/api';

// ==================== GENERIC API HOOK ====================

export const useApi = (apiFunction, dependencies = [], immediate = true) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (...args) => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiFunction(...args);
        setData(result);
        return result;
      } catch (err) {
        setError(err.message || 'An error occurred');
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, dependencies);

  return { data, loading, error, execute, refetch: execute };
};

// ==================== EQUIPMENT HOOKS ====================

export const useEquipment = (filters = {}, immediate = true) => {
  return useApi(
    () => apiService.getEquipment(filters),
    [JSON.stringify(filters)],
    immediate
  );
};

export const useEquipmentById = (id, immediate = true) => {
  return useApi(
    () => apiService.getEquipmentById(id),
    [id],
    immediate
  );
};

export const useEquipmentStatus = (immediate = true) => {
  return useApi(
    () => apiService.getEquipmentStatus(),
    [],
    immediate
  );
};

export const useEquipmentReadings = (id, filters = {}, immediate = true) => {
  return useApi(
    () => apiService.getEquipmentReadings(id, filters),
    [id, JSON.stringify(filters)],
    immediate
  );
};

export const useEquipmentAlerts = (id, immediate = true) => {
  return useApi(
    () => apiService.getEquipmentAlerts(id),
    [id],
    immediate
  );
};

// ==================== EQUIPMENT TYPES HOOKS ====================

export const useEquipmentTypes = (immediate = true) => {
  return useApi(
    () => apiService.getEquipmentTypes(),
    [],
    immediate
  );
};

// ==================== PLANT LOCATIONS HOOKS ====================

export const usePlantLocations = (immediate = true) => {
  return useApi(
    () => apiService.getPlantLocations(),
    [],
    immediate
  );
};

// ==================== READINGS HOOKS ====================

export const useReadings = (filters = {}, immediate = true) => {
  return useApi(
    () => apiService.getReadings(filters),
    [JSON.stringify(filters)],
    immediate
  );
};

// ==================== ALERTS HOOKS ====================

export const useAlerts = (filters = {}, immediate = true) => {
  return useApi(
    () => apiService.getAlerts(filters),
    [JSON.stringify(filters)],
    immediate
  );
};

// ==================== DASHBOARD HOOKS ====================

export const useDashboardStats = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getDashboardStats(params),
    [JSON.stringify(params)],
    immediate
  );
};

export const useDashboardOverview = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getDashboardOverview(params),
    [JSON.stringify(params)],
    immediate
  );
};

// ==================== CHARTS HOOKS ====================

export const useCharts = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getCharts(params),
    [JSON.stringify(params)],
    immediate
  );
};

export const useEquipmentChartData = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getEquipmentChartData(params),
    [JSON.stringify(params)],
    immediate
  );
};

export const usePressureTrends = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getPressureTrends(params),
    [JSON.stringify(params)],
    immediate
  );
};

export const useTemperatureTrends = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getTemperatureTrends(params),
    [JSON.stringify(params)],
    immediate
  );
};

// ==================== UPLOAD HISTORY HOOKS ====================

export const useUploadHistory = (filters = {}, immediate = true) => {
  return useApi(
    () => apiService.getUploadHistory(filters),
    [JSON.stringify(filters)],
    immediate
  );
};

// ==================== ANALYTICS HOOKS ====================

export const useAnalytics = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getAnalytics(params),
    [JSON.stringify(params)],
    immediate
  );
};

export const useEquipmentAnalytics = (id, params = {}, immediate = true) => {
  return useApi(
    () => apiService.getEquipmentAnalytics(id, params),
    [id, JSON.stringify(params)],
    immediate
  );
};

// ==================== STATISTICS HOOKS ====================

export const useStatistics = (params = {}, immediate = true) => {
  return useApi(
    () => apiService.getStatistics(params),
    [JSON.stringify(params)],
    immediate
  );
};

// ==================== AUTH HOOKS ====================

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        if (apiService.getToken()) {
          const userData = await apiService.getCurrentUser();
          setUser(userData);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const login = async (username, password) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.login(username, password);
      const userData = await apiService.getCurrentUser();
      setUser(userData);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await apiService.logout();
      setUser(null);
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
  };
};

// ==================== FILE UPLOAD HOOK ====================

export const useFileUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  const uploadFile = async (file, metadata = {}) => {
    try {
      setUploading(true);
      setError(null);
      setProgress(0);

      // Simulate progress (in real implementation, use XMLHttpRequest for progress)
      const interval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const result = await apiService.uploadFile(file, metadata);
      
      clearInterval(interval);
      setProgress(100);
      
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  return { uploadFile, uploading, progress, error };
};

// ==================== MUTATION HOOK (for create, update, delete) ====================

export const useMutation = (mutationFunction) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const mutate = useCallback(
    async (...args) => {
      try {
        setLoading(true);
        setError(null);
        const result = await mutationFunction(...args);
        setData(result);
        return result;
      } catch (err) {
        setError(err.message || 'An error occurred');
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [mutationFunction]
  );

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setData(null);
  }, []);

  return { mutate, loading, error, data, reset };
};

// ==================== POLLING HOOK ====================

export const usePolling = (apiFunction, interval = 5000, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    let timeoutId;

    const fetchData = async () => {
      try {
        const result = await apiFunction();
        if (isMounted) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
          timeoutId = setTimeout(fetchData, interval);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [...dependencies, interval]);

  return { data, loading, error };
};
