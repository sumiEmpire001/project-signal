"""Evaluate task completion, blocking and overdue project risks."""
import argparse
import json
import sys
from datetime import date

STATES={"todo","in_progress","blocked","done"}

def evaluate(tasks,today=None):
    if not isinstance(tasks,list): raise ValueError("tasks must be a list")
    today=today or date.today()
    total=len(tasks)
    done=blocked=overdue=0
    issues=[]
    for i,task in enumerate(tasks):
        if not isinstance(task,dict) or task.get("status") not in STATES:
            raise ValueError("invalid task status at index "+str(i))
        state=task["status"]
        done+=state=="done"
        blocked+=state=="blocked"
        if task.get("due"):
            try: due=date.fromisoformat(task["due"])
            except (ValueError,TypeError): raise ValueError("invalid due date at index "+str(i))
            if due<today and state!="done":
                overdue+=1
                issues.append({"index":i,"issue":"overdue"})
        if state=="blocked": issues.append({"index":i,"issue":"blocked"})
    score=max(0,min(100,round(100*(done/total if total else 1)-10*blocked-5*overdue)))
    return {"total":total,"done":done,"blocked":blocked,"overdue":overdue,"score":score,"issues":issues}

def main(argv=None):
    p=argparse.ArgumentParser(description="Summarize project task health")
    p.add_argument("file")
    p.add_argument("--today",help="Override date YYYY-MM-DD")
    args=p.parse_args(argv)
    try:
        with open(args.file,encoding="utf-8") as f: data=json.load(f)
        if not isinstance(data,dict): raise ValueError("input must be an object")
        today=date.fromisoformat(args.today) if args.today else None
        result=evaluate(data.get("tasks"),today)
    except (OSError,ValueError,TypeError) as exc:
        print(str(exc),file=sys.stderr)
        return 2
    print(json.dumps(result,indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
