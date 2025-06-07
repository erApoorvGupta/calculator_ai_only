"use client";

import React from 'react';

interface ButtonProps {
  label: string | React.ReactNode;
  onClick: () => void;
  type?: "number" | "operator" | "action" | "scientific";
  className?: string;
  gridSpan?: number; // For buttons like '0' or '=' that might span columns
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  type = "number",
  className = "",
  gridSpan,
}) => {
  let baseStyle = "aspect-square rounded-md flex items-center justify-center text-xl sm:text-2xl focus:outline-none transition-colors duration-150 font-medium";

  if (type === "number") {
    baseStyle += " bg-[var(--color-grey-light)] text-black hover:bg-[var(--color-grey-medium)] active:bg-[var(--color-grey-dark)]";
  } else if (type === "operator") {
    baseStyle += " bg-[var(--color-accent-orange)] text-white hover:bg-orange-600 active:bg-orange-700";
  } else if (type === "action") {
    baseStyle += " bg-[var(--color-grey-dark)] text-white hover:bg-gray-600 active:bg-gray-700";
  } else if (type === "scientific") {
    baseStyle += " bg-gray-700 text-white hover:bg-gray-600 active:bg-gray-500 text-lg sm:text-xl"; // Slightly smaller text for scientific
  }

  if (gridSpan) {
    baseStyle += ` col-span-${gridSpan}`;
  }

  return (
    <button
      onClick={onClick}
      className={`${baseStyle} ${className}`}
    >
      {label}
    </button>
  );
};

export default Button;
