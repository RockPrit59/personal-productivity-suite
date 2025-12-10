# notes_manager.py
from utils import NOTES_FILE, read_json, write_json, now_str
from typing import List, Dict, Any

class NotesManager:
    def list_notes(self) -> List[Dict[str, Any]]:
        data = read_json(NOTES_FILE, [])
        return data or []

    def add_note(self, title: str, content: str) -> Dict[str, Any]:
        notes = self.list_notes()
        nid = max((n.get("id", 0) for n in notes), default=0) + 1
        note = {"id": nid, "title": title, "content": content, "created": now_str(), "modified": now_str()}
        notes.append(note)
        write_json(NOTES_FILE, notes)
        return note

    def find(self, query: str):
        q = query.lower()
        return [n for n in self.list_notes() if q in n.get("title", "").lower() or q in n.get("content", "").lower()]

    def get(self, nid: int):
        for n in self.list_notes():
            if n.get("id") == nid:
                return n
        return None

    def edit(self, nid: int, title: str = None, content: str = None) -> bool:
        notes = self.list_notes()
        changed = False
        for n in notes:
            if n.get("id") == nid:
                if title is not None:
                    n["title"] = title
                if content is not None:
                    n["content"] = content
                n["modified"] = now_str()
                changed = True
                break
        if changed:
            write_json(NOTES_FILE, notes)
        return changed

    def delete(self, nid: int) -> bool:
        notes = self.list_notes()
        new = [n for n in notes if n.get("id") != nid]
        if len(new) != len(notes):
            write_json(NOTES_FILE, new)
            return True
        return False

    def export(self, path: str, fmt: str = "txt") -> str:
        fmt = fmt.lower()
        notes = self.list_notes()
        if fmt == "txt":
            with open(path, "w", encoding="utf-8") as f:
                for n in notes:
                    f.write(f"ID: {n['id']} | {n['title']} | Created: {n['created']}\n")
                    f.write(n["content"] + "\n\n")
        elif fmt == "csv":
            import csv
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["id", "title", "content", "created", "modified"])
                for n in notes:
                    w.writerow([n["id"], n["title"], n["content"], n["created"], n["modified"]])
        elif fmt == "json":
            write_json(path, notes)
        else:
            raise ValueError("Unsupported format")
        return path
