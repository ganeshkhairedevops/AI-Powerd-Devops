function SearchBar({ value, onChange }) {
    return (
        <input
            type="text"
            placeholder="?? Search chats..."
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 text-sm text-white placeholder-gray-400 outline-none focus:border-blue-500"
        />
    );
}

export default SearchBar;