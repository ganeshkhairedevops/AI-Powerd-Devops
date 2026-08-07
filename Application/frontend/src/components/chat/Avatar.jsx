import { FaRobot, FaUser } from "react-icons/fa";

export default function Avatar({ role }) {
  const isUser = role === "user";

  return (
    <div
      className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${
        isUser
          ? "bg-cyan-600 text-white"
          : "bg-slate-700 text-cyan-400"
      }`}
    >
      {isUser ? <FaUser size={18} /> : <FaRobot size={18} />}
    </div>
  );
}