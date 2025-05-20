import json
import fitz
from .models import  *

def get_notes(course: Course, as_json = False):
    """
    Function that takes in a course(ORM object) and returns the notes as 
    a string or string in JSON format that includes the title and the content.

    Args:
        course (Course): Course model instance
        as_json (bool): If True, returns text as JSON string, otherwise as regular string

    Returns:
        the notes as a string or string in JSON format
    """
    # fetch all notes from the Course
    notes = course.notes.all()

    # check for empty notes
    if not notes:
        return "" if not as_json else "[]"
    
    # format the output based on string or json
    if not as_json:
        str_notes = ""
        for note in notes:
            str_notes += f"Title: {note.title}\n"
            str_notes += f"Contents: {note.content}\n\n"
        return str_notes
    else:
        json_notes = [{"Title": note.title, "Contents": note.content} for note in notes]
        return json.dumps(json_notes)



def get_syllabus(course: Course, as_json=False):
    """
    Extract text from a course's syllabus PDF file.

    Args:
        course (Course): Course model instance containing a syllabus PDF
        as_json (bool): If True, returns text as JSON string, otherwise as regular string

    Returns:
        str: The extracted text from the syllabus PDF
    """

    if not course.syllabus or not course.syllabus.name:
        return "" if not as_json else json.dumps({"error": "No syllabus found"})

    try:
        # Open with .open('rb') for storage backend safety
        with course.syllabus.open("rb") as file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

        return json.dumps({"syllabus_text": text}) if as_json else text

    except Exception as e:
        error_message = f"Error extracting syllabus text: {str(e)}"
        return error_message if not as_json else json.dumps({"error": error_message})
