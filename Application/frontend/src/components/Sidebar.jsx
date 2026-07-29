import {
  FaDocker,
  FaLinux,
  FaGithub,
  FaAws,
  FaCog,
  FaRobot,
} from "react-icons/fa";

import {
    SiKubernetes,
    SiTerraform,
    SiJenkins,
    SiHelm,
    SiAnsible,
} from "react-icons/si";

import ChatHistory from "./ChatHistory";

function Sidebar() {
    const tools = [
        { name: "Kubernetes", icon: <SiKubernetes /> },
        { name: "Docker", icon: <FaDocker /> },
        { name: "Linux", icon: <FaLinux /> },
        { name: "AWS", icon: <FaAws /> },
        { name: "GitHub", icon: <FaGithub /> },
        { name: "Terraform", icon: <SiTerraform /> },
        { name: "Helm", icon: <SiHelm /> },
        { name: "Jenkins", icon: <SiJenkins /> },
        { name: "Ansible", icon: <SiAnsible /> },
    ];

    return (
        <aside className="w-72 h-screen bg-slate-900 border-r border-slate-700 flex flex-col">

            <div className="p-5 border-b border-slate-700">
                <h1 className="flex items-center gap-2 text-xl font-bold">
                     <FaRobot className="text-cyan-400" />
                     DevOps AI Agent
                </h1>
                <p className="text-xs text-gray-400 mt-1">
                    AI Powered DevOps Assistant
                </p>
            </div>

            <div className="p-4 overflow-y-auto flex-1">
                <ChatHistory />

                <div className="mt-8">
                    <h3 className="text-xs uppercase text-gray-400 mb-3">
                        DevOps Tools
                    </h3>

                    <div className="space-y-2">
                        {tools.map((tool) => (
                            <button
                                key={tool.name}
                                className="w-full flex items-center gap-3 rounded-lg px-3 py-2 hover:bg-slate-800 transition"
                            >
                                {tool.icon}
                                <span>{tool.name}</span>
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            <div className="border-t border-slate-700 p-4">
                <button className="w-full flex items-center gap-3 rounded-lg px-3 py-2 hover:bg-slate-800 transition">
                    <FaCog />
                    Settings
                </button>
            </div>
        </aside>
    );
}

export default Sidebar;