function HistoryItem({

    title,

    active,

    onClick

}) {

    return (

        <button

            onClick={onClick}

            className={`

            w-full

            text-left

            p-3

            rounded-lg

            mb-2

            transition

            ${

                active

                    ? "bg-cyan-700"

                    : "hover:bg-slate-700"

            }

            `}

        >

            ?? {title}

        </button>

    );

}

export default HistoryItem;