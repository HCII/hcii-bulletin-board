class HomeController < ApplicationController
  def login
    if session[:return_to].nil?
      session[:return_to] = request.referer
    end
  end
  
  def authenticate
    if params[:password] == ENV['SIMPLE_AUTH_PASSWORD']
      session[:authorized] = true
      flash[:notice] = "You're logged in!"
      redirect_to (session[:return_to] ? session[:return_to] : root_path)
      session[:return_to] = nil
    else
      flash[:notice] = "Incorrect password."
      redirect_to login_path
    end
  end
  
  def logout
    flash[:notice] = "You're logged out!"
    session[:authorized] = false
    redirect_to root_path
  end
end
