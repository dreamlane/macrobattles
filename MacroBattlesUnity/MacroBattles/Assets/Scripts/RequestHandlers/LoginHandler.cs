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
      // For some reason, chunked transfer does not work with the server.
      www.chunkedTransfer = false;
      yield return www.Send();

      if(www.isNetworkError) {
        errorText.text = "Connection Error";
        Debug.LogError(www.error);
      } else {
        string rawjson = www.downloadHandler.text;
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        handleResponse(response);
      }
    }
  }

  void handleRegisterClick() {
    StartCoroutine(uploadRegisterForm());
  }

  IEnumerator uploadRegisterForm() {
    // TODO: DRY this up with the uploadLoginForm.
    WWWForm form = new WWWForm();
    form.AddField("username", usernameField.text);
    form.AddField("password", passwordField.text);
    using(UnityWebRequest www = UnityWebRequest.Post(requestDomain + "/register", form)) {
      // For some reason, chunked transfer does not work with the server.
      www.chunkedTransfer = false;
      yield return www.Send();

      if(www.isNetworkError) {
        errorText.text = "Connection Error";
        Debug.LogError(www.error);
      }
      else {
        string rawjson = www.downloadHandler.text;
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        handleResponse(response);
      }
    }
  }

  private void handleResponse(ResponseModel response) {
    if (response.status == ResponseConstants.SUCCESS) {
      // Set the initial PlayerModel on the GameState.
      PlayerModel playerModel = JsonUtility.FromJson<PlayerModel>(response.data);
      GameState.SetCurrentPlayerModel(playerModel);
      SceneManager.LoadScene("GameScene", LoadSceneMode.Single);
    } else {
      // If Login doesn't work, expose the error message to the user.
      errorText.text = response.error;
    }
  }
}
