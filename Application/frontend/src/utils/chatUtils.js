// src/utils/chatUtils.js

const STORAGE_KEY = "devops-ai-chats";

/**
 * Generate a chat title from the user's first prompt.
 */
export function generateTitle(prompt = "") {

    const text = prompt.toLowerCase().trim();

    // Docker
    if (text.includes("container"))
        return "Docker Containers";

    if (text.includes("docker"))
        return "Docker";

    // Kubernetes
    if (text.includes("deployment"))
        return "Kubernetes Deployment";

    if (text.includes("service"))
        return "Kubernetes Service";

    if (text.includes("pod"))
        return "Kubernetes Pods";

    if (
        text.includes("kubernetes") ||
        text.includes("kubectl")
    )
        return "Kubernetes";

    // AWS
    if (text.includes("ec2"))
        return "EC2 Instances";

    if (text.includes("eks"))
        return "EKS Cluster";

    if (text.includes("s3"))
        return "S3 Bucket";

    if (text.includes("iam"))
        return "IAM";

    if (text.includes("vpc"))
        return "VPC";

    if (text.includes("aws"))
        return "AWS";

    // Terraform
    if (text.includes("terraform"))
        return "Terraform";

    // Linux
    if (text.includes("linux"))
        return "Linux";

    // Jenkins
    if (text.includes("jenkins"))
        return "Jenkins";

    // Helm
    if (text.includes("helm"))
        return "Helm";

    // Ansible
    if (text.includes("ansible"))
        return "Ansible";

    // GitHub
    if (text.includes("github"))
        return "GitHub";

    // Git
    if (text.includes("git"))
        return "Git";

    // Prometheus
    if (text.includes("prometheus"))
        return "Prometheus";

    // Grafana
    if (text.includes("grafana"))
        return "Grafana";

    // Default title
    return prompt
        .trim()
        .split(/\s+/)
        .slice(0, 5)
        .join(" ");
}

/**
 * Save all conversations.
 */
export function saveChats(chats) {

    try {

        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(chats)
        );

    } catch (err) {

        console.error("Unable to save chats", err);

    }

}

/**
 * Load conversations.
 */
export function loadChats() {

    try {

        const chats = localStorage.getItem(STORAGE_KEY);

        return chats ? JSON.parse(chats) : [];

    } catch (err) {

        console.error("Unable to load chats", err);

        return [];

    }

}

/**
 * Remove all conversations.
 */
export function clearChats() {

    localStorage.removeItem(STORAGE_KEY);

}

/**
 * Search conversations.
 */
export function searchChats(conversations, keyword) {

    if (!keyword) return conversations;

    return conversations.filter(chat =>
        chat.title
            .toLowerCase()
            .includes(keyword.toLowerCase())
    );

}

/**
 * Sort conversations by latest update.
 */
export function sortChats(conversations) {

    return [...conversations].sort(
        (a, b) =>
            new Date(b.updatedAt) -
            new Date(a.updatedAt)
    );

}