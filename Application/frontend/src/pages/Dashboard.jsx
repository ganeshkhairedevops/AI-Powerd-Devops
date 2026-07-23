import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

function Dashboard() {
  return (
    <div className="h-screen bg-slate-950 text-white">

      <Header />

      <div className="flex h-[calc(100vh-64px)]">

        <Sidebar />

        <ChatWindow />

      </div>

    </div>
  );
}

export default Dashboard;