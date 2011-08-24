class ApplicationController < ActionController::Base
  
  # Include all helpers, all the time
  helper :all
  
  protect_from_forgery
  
  private
  
  def auth_required
    unless session[:authorized]
      flash[:notice] = "You need to be logged in."
      redirect_to login_path
    end
  end
end
