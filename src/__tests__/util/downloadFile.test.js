import { vi } from 'vitest';
// import { screen } from '@testing-library/react';
import { downloadPdf } from '../../util/downloadFile'; // Import your utility functions here

describe('File Download Utility Functions', () => {
  it('should download a PDF file', () => {
    // Mock Blob and createObjectURL
    window.Blob = vi.fn();
    window.URL.createObjectURL = vi.fn(() => 'test-object-url');

    const pdfData = 'Mock PDF Data';
    const pdfFilename = 'sample.pdf';

    // Mock the createElement and click methods for the link element
    const createElementMock = vi.spyOn(document, 'createElement').mockImplementation(() => {
      return {
        href: '',
        download: '',
        click: vi.fn(),
        remove: vi.fn(),
      };
    });

    // const mockDownload = vi.fn().mockImplementation(downloadPdf);
    // const fakeDl = mockDownload(pdfData, pdfFilename);
    // console.log(fakeDl);
    downloadPdf(pdfData, pdfFilename);

    // Assertions
    expect(window.Blob).toHaveBeenCalledWith([pdfData], { type: 'application/pdf' });
    expect(window.URL.createObjectURL).toHaveBeenCalledWith(new Blob([pdfData], { type: 'application/pdf' }));

    expect(createElementMock).toHaveBeenCalledWith('a');
    // expect(createElementMock.download).toBe(pdfFilename);
    // expect(createElementMock.href).toBe('test-object-url');

    createElementMock.mockRestore();
  });
});
