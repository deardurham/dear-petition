export const downloadPdf = (pdf, filename) => {
  downloadFile(pdf, filename, 'application/pdf');
};

export const downloadFile = (data, filename, filetype) => {
  const fileBlob = new Blob([data], { type: filetype });
  const url = window.URL.createObjectURL(fileBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => {
    window.URL.revokeObjectURL(url);
    link.remove();
  });
};
