import React from "react";

export const PlannerLogo = () => {
  return (
    <svg
      width="40"
      height="40"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* A simple calendar icon */}
      <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="2" />
      <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" strokeWidth="2" />
      <line x1="7" y1="2" x2="7" y2="6" stroke="currentColor" strokeWidth="2" />
      <line x1="17" y1="2" x2="17" y2="6" stroke="currentColor" strokeWidth="2" />
    </svg>
  );
};
