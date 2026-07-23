import {
  FaDocker,
  FaLinux,
  FaGithub,
  FaAws,
} from "react-icons/fa";

import {
  SiKubernetes,
  SiTerraform,
  SiJenkins,
  SiHelm,
  SiAnsible,
} from "react-icons/si";

function Sidebar() {
  const items = [
    ["Kubernetes", <SiKubernetes />],
    ["Docker", <FaDocker />],
    ["Linux", <FaLinux />],
    ["AWS", <FaAws />],
    ["GitHub", <FaGithub />],
    ["Terraform", <SiTerraform />],
    ["Helm", <SiHelm />],
    ["Jenkins", <SiJenkins />],
    ["Ansible", <SiAnsible />],
  ];

  return (
    <aside className="w-72 bg-slate-900 border-r border-slate-700 p-5">
      <h2 className="font-bold text-xl mb-6">
        DevOps Tools
      </h2>

      <div className="space-y-3">
        {items.map(([name, icon]) => (
          <button
            key={name}
            className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 transition"
          >
            {icon}
            {name}
          </button>
        ))}
      </div>
    </aside>
  );
}

export default Sidebar;