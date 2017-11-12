using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

#if UNITY_EDITOR
using UnityEditor;
#endif

public class LoginHandler : MonoBehaviour {

  public InputField usernameField;
  public InputField passwordField;
  // Used to display login errors to the user.
  public Text errorText;
  public Button loginButton;
  public Button registerButton;
  private string requestDomain = Constants.APP_DOMAIN;

  void Start() {
    loginButton.GetComponent<Button>().onClick.AddListener(handleLoginClick);
    registerButton.GetComponent<Button>().onClick.AddListener(handleRegisterClick);

#if UNITY_EDITOR
    if (EditorApplication.isPlayingOrWillChangePlaymode) {
      requestDomain = Constants.LOCAL_HOST;
    }
#endif
  }
	// Use this for initialization
	void handleLoginClick() {
    StartCoroutine(uploadLoginForm());
  }

  IEnumerator uploadLoginForm() {
    WWWForm form = new WWWForm();
    form.AddField("username", usernameField.text);
    form.AddField("password", passwordField.text);

    using(UnityWebRequest www = UnityWebRequest.Post(requestDomain + "/login", form)) {
      yield return www.Send();

      if(www.isError) {
        errorText.text = "Connection Error";
        Debug.Log(www.error);
      } else {
        string rawjson = www.downloadHandler.text;
        Debug.Log("Form upload complete!");
        Debug.Log(www.downloadHandler.text);
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        if (response.status == ResponseConstants.SUCCESS) {
          SceneManager.LoadScene("GameScene", LoadSceneMode.Single);
        } else {
          errorText.text = response.error;
          Debug.Log(response.status);
          Debug.Log(response.data);
          Debug.Log(response.error);
        }
      }
    }
  }

  void handleRegisterClick() {
    StartCoroutine(uploadRegisterForm());
  }

  IEnumerator uploadRegisterForm() {
    WWWForm form = new WWWForm();
    form.AddField("username", usernameField.text);
    form.AddField("password", passwordField.text);
    using(UnityWebRequest www = UnityWebRequest.Post(requestDomain + "/register", form)) {
      Debug.Log("SENDING");
      yield return www.Send();

      if(www.isError) {
        errorText.text = "Connection Error";
        Debug.Log(www.error);
      }
      else {
        string rawjson = www.downloadHandler.text;
        Debug.Log("Form upload complete!");
        Debug.Log(www.downloadHandler.text);
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        if (response.status == ResponseConstants.SUCCESS) {
          SceneManager.LoadScene("GameScene", LoadSceneMode.Single);
        } else {
          errorText.text = response.error;
          Debug.Log(response.status);
          Debug.Log(response.data);
          Debug.Log(response.error);
        }
      }
    }
  }
}
