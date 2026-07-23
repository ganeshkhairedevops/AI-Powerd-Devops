from langchain_core.tools import tool
from utils.command_runner import run_command


@tool
def aws_identity():
    """Show current AWS identity."""
    return run_command(["aws", "sts", "get-caller-identity"])


@tool
def aws_regions():
    """List AWS regions."""
    return run_command([
        "aws",
        "ec2",
        "describe-regions",
        "--query",
        "Regions[*].RegionName",
        "--output",
        "table",
    ])


@tool
def ec2_instances():
    """List EC2 instances."""
    return run_command([
        "aws",
        "ec2",
        "describe-instances",
        "--output",
        "table",
    ])


@tool
def eks_clusters():
    """List EKS clusters."""
    return run_command([
        "aws",
        "eks",
        "list-clusters",
    ])


@tool
def s3_buckets():
    """List S3 buckets."""
    return run_command([
        "aws",
        "s3",
        "ls",
    ])


@tool
def iam_users():
    """List IAM users."""
    return run_command([
        "aws",
        "iam",
        "list-users",
    ])


@tool
def vpcs():
    """List VPCs."""
    return run_command([
        "aws",
        "ec2",
        "describe-vpcs",
        "--output",
        "table",
    ])