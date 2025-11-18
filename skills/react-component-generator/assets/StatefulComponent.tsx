import React from 'react';
import { create } from 'zustand';

// Define the store interface
interface ComponentNameStore {
  // State
  count: number;
  isLoading: boolean;

  // Actions
  increment: () => void;
  decrement: () => void;
  setLoading: (loading: boolean) => void;
  reset: () => void;
}

// Create the Zustand store
export const useComponentNameStore = create<ComponentNameStore>((set) => ({
  // Initial state
  count: 0,
  isLoading: false,

  // Actions
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  setLoading: (loading) => set({ isLoading: loading }),
  reset: () => set({ count: 0, isLoading: false }),
}));

interface ComponentNameProps {
  className?: string;
}

/**
 * ComponentName - A component with Zustand state management
 *
 * @param props - Component props
 * @returns JSX.Element
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  className = ''
}) => {
  const { count, isLoading, increment, decrement, reset } = useComponentNameStore();

  return (
    <div className={`/* Add Tailwind classes here */ ${className}`}>
      <p className="text-lg font-semibold">Count: {count}</p>

      <div className="flex gap-2 mt-4">
        <button
          onClick={increment}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          Increment
        </button>

        <button
          onClick={decrement}
          disabled={isLoading}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
        >
          Decrement
        </button>

        <button
          onClick={reset}
          disabled={isLoading}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 disabled:opacity-50"
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default ComponentName;
