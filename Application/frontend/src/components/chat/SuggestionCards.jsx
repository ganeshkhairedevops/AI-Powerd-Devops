import {
  FaDocker,
  FaAws,
  FaGithub,
} from "react-icons/fa";

import {
  SiKubernetes,
  SiTerraform,
} from "react-icons/si";

const suggestions = [
  {
    icon: <FaDocker />,
    title: "Show running Docker containers",
    prompt: "Show running Docker containers",
  },
  {
    icon: <SiKubernetes />,
    title: "List Kubernetes pods",
    prompt: "List Kubernetes pods",
  },
  {
    icon: <FaAws />,
    title: "List EC2 instances",
    prompt: "List AWS EC2 instances",
  },
  {
    icon: <SiTerraform />,
    title: "Explain Terraform plan",
    prompt: "Explain a Terraform plan",
  },
  {
    icon: <FaGithub />,
    title: "Show GitHub repository status",
    prompt: "Show GitHub repository status",
  },
];

export default function SuggestionCards({ onSelect }) {
  return (
    <div className="mt-10 grid gap-4 md:grid-cols-2">
      {suggestions.map((item) => (
        <button
          key={item.title}
          onClick={() => onSelect(item.prompt)}
          className="rounded-xl border border-slate-700 bg-slate-900 p-5 text-left transition hover:border-cyan-500 hover:bg-slate-800"
        >
          <div className="mb-3 text-2xl text-cyan-400">
            {item.icon}
          </div>

          <h3 className="font-semibold text-white">
            {item.title}
          </h3>
        </button>
      ))}
    </div>
  );
}