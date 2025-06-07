"use client";

interface DisplayProps {
  value: string;
  expression?: string; // Optional: to show the full expression or history
}

const Display: React.FC<DisplayProps> = ({ value, expression }) => {
  return (
    <div className="w-full bg-[var(--color-grey-medium)] rounded-md mb-4 p-4 text-right overflow-hidden">
      {expression && (
        <div className="text-sm text-gray-700 dark:text-gray-400 h-6 truncate">
          {expression}
        </div>
      )}
      <div
        className="text-4xl sm:text-5xl text-black break-all font-mono"
        style={{ wordBreak: 'break-all' }} // Ensure long numbers wrap or break
      >
        {value}
      </div>
    </div>
  );
};

export default Display;
