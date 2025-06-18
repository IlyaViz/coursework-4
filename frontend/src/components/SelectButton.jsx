const SelectButton = ({ selected, children, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`p-1 rounded-lg ${selected ? "bg-blue-400" : "bg-gray-300"}`}
    >
      {children}
    </button>
  );
};

export default SelectButton;
