import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { SectionHeader, ToggleSwitch, StatusBadge } from './index';
import { UncertaintyCaliper } from '../upload/UncertaintyCaliper';

describe('Common UI Components', () => {
  test('SectionHeader renders title, subtitle and badge', () => {
    render(
      <SectionHeader 
        title="Clinical Diagnostic Triage" 
        subtitle="Automated histological grading"
        badge="v2.1"
      />
    );
    expect(screen.getByText('Clinical Diagnostic Triage')).toBeInTheDocument();
    expect(screen.getByText('Automated histological grading')).toBeInTheDocument();
    expect(screen.getByText('v2.1')).toBeInTheDocument();
  });

  test('ToggleSwitch toggles value on click', () => {
    const handleChange = jest.fn();
    render(
      <ToggleSwitch 
        id="cross-pol" 
        label="Cross-Polarized Lighting" 
        checked={false} 
        onChange={handleChange} 
      />
    );
    expect(screen.getByText('Cross-Polarized Lighting')).toBeInTheDocument();
    const btn = screen.getByRole('switch');
    fireEvent.click(btn);
    expect(handleChange).toHaveBeenCalledWith(true);
  });

  test('StatusBadge displays correct text and styles for cancer and non_cancer', () => {
    const { rerender } = render(<StatusBadge type="cancer" />);
    expect(screen.getByText('High Risk / Malignant')).toBeInTheDocument();

    rerender(<StatusBadge type="non_cancer" />);
    expect(screen.getByText('Benign / Non-Cancerous')).toBeInTheDocument();

    rerender(<StatusBadge type="uncertain" />);
    expect(screen.getByText('Equivocal / Inconclusive')).toBeInTheDocument();
  });

  test('UncertaintyCaliper renders epistemic uncertainty stats', () => {
    render(
      <UncertaintyCaliper 
        confidence={0.92} 
        uncertainty={0.0045} 
        prediction="cancer" 
      />
    );
    expect(screen.getByText(/EPISTEMIC UNCERTAINTY CALIPER/i)).toBeInTheDocument();
    expect(screen.getByText(/STABLE CONSENSUS/i)).toBeInTheDocument();
  });
});
