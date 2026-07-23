function Header() {
  return (
    <header className="h-16 bg-slate-900 border-b border-slate-700 flex items-center justify-between px-6">
      <h1 className="text-2xl font-bold text-cyan-400">
        ?? DevOps AI Agent
      </h1>

      <div className="flex gap-4">
        <span className="text-green-400">?? Connected</span>
      </div>
    </header>
  );
}

export default Header;