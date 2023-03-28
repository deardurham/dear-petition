export default function downloadPdf(pdf, filename) {
  const pdfBlob = new Blob([pdf], { type: 'application/pdf' });
  const url = window.URL.createObjectURL(pdfBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => {
    window.URL.revokeObjectURL(url);
    link.remove();
  });
}
