const generateServiceColor = (serviceName) => {
  const hash = Array.from(serviceName).reduce((acc, char) => {
    return acc + char.charCodeAt(0);
  }, 0);

  const hue = hash % 360; // Ensure hue is between 0 and 360
  return `hsl(${hue}, 70%, 50%)`; // Saturation and lightness can be adjusted
};

export default generateServiceColor;
