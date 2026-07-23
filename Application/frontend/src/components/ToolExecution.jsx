function ToolExecution({ tool, command, execution }) {

    return (

        <div className="bg-slate-900 border-t border-slate-700 p-5">

            <h3 className="font-bold mb-4">
                ? Tool Execution
            </h3>

            <div className="space-y-2 text-sm">

                <p>

                    <b>Tool :</b> {tool}

                </p>

                <p>

                    <b>Command :</b>

                </p>

                <pre className="bg-slate-950 p-3 rounded">

                    {command}

                </pre>

                <p>

                    <b>Execution :</b> {execution}s

                </p>

            </div>

        </div>

    );

}

export default ToolExecution;