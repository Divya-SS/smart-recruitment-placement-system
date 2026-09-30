import React from 'react';

export default function MatchProgressBar({ score, showLabel = true, size = 'md' }) {
  const numScore = parseFloat(score) || 0;

  // Determine color scheme based on score thresholds
  let color = 'bg-rose-500';
  let textColor = 'text-rose-700';
  let bgTrack = 'bg-rose-100';

  if (numScore >= 75) {
    color = 'bg-emerald-500';
    textColor = 'text-emerald-700';
    bgTrack = 'bg-emerald-100';
  } else if (numScore >= 50) {
    color = 'bg-amber-500';
    textColor = 'text-amber-700';
    bgTrack = 'bg-amber-100';
  }

  const heightClass = size === 'sm' ? 'h-1.5' : size === 'lg' ? 'h-3.5' : 'h-2.5';

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs font-semibold text-slate-600">Match Score</span>
          <span className={`text-xs font-bold ${textColor}`}>{numScore.toFixed(1)}%</span>
        </div>
      )}
      <div className={`w-full ${bgTrack} rounded-full overflow-hidden ${heightClass}`}>
        <div
          className={`${color} ${heightClass} rounded-full transition-all duration-500`}
          style={{ width: `${Math.min(100, Math.max(0, numScore))}%` }}
        />
      </div>
    </div>
  );
}
