from AGSM.Data_manipulation_and_plotting import EMG

def check_ref_label_removel():
    labels = ["Biceps","ref","Triceps"]
    filtered_labels = ["Biceps","Triceps"]
    q = EMG(labels)
    assert filtered_labels == q.labels


if __name__ == "__main__":
    test_functions = ["check_ref_label_removel"]
    errors = []

    for func in test_functions:
        try:
            eval(func)()
        except Exception as e:
            errors.append(f"Failed when testing method '{func}': {e}")
    if len(errors) > 0:
        print(errors)
    else:
        print("Tests pass successfully.")
