import React from 'react';

interface ListItem {
  id: string | number;
  title: string;
  description?: string;
}

interface ComponentNameProps {
  items: ListItem[];
  onItemClick?: (item: ListItem) => void;
  onItemDelete?: (id: string | number) => void;
  className?: string;
  emptyMessage?: string;
}

/**
 * ComponentName - A reusable list component
 *
 * @param props - Component props
 * @returns JSX.Element
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  items,
  onItemClick,
  onItemDelete,
  className = '',
  emptyMessage = 'No items to display'
}) => {
  if (items.length === 0) {
    return (
      <div className={`text-center py-8 text-gray-500 ${className}`}>
        {emptyMessage}
      </div>
    );
  }

  return (
    <ul className={`space-y-2 ${className}`}>
      {items.map((item) => (
        <li
          key={item.id}
          className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
        >
          <div
            className={`flex-1 ${onItemClick ? 'cursor-pointer' : ''}`}
            onClick={() => onItemClick?.(item)}
          >
            <h3 className="text-lg font-semibold text-gray-900">
              {item.title}
            </h3>
            {item.description && (
              <p className="mt-1 text-sm text-gray-600">
                {item.description}
              </p>
            )}
          </div>

          {onItemDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onItemDelete(item.id);
              }}
              className="ml-4 px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
              aria-label={`Delete ${item.title}`}
            >
              Delete
            </button>
          )}
        </li>
      ))}
    </ul>
  );
};

export default ComponentName;
