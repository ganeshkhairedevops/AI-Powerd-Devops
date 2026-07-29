import { FaSearch } from "react-icons/fa"
function SearchBar({ value, onChange }) {
    return (
        <div className="relative">
            <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
                type="text"
                placeholder="Search chats..."
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full pl-10 pr-3 py-2 rounded-lg bg-slate-800"
            />
        </div>
    );
}

export default SearchBar;